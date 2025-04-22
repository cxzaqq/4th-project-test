<template>
    <div id="canvas-container" style="width: 100%; height: 600px"></div>
</template>

<script setup>
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { onMounted } from "vue";

onMounted(() => {
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
        45,
        window.innerWidth / 600,
        0.2,
        3000
    );
    camera.position.set(0, 5, 20);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, 600);
    renderer.setPixelRatio(window.devicePixelRatio);
    document
        .getElementById("canvas-container")
        .appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    scene.add(directionalLight);

    const loader = new GLTFLoader();
    const files = ["pink-tree.glb", "peng.glb", "hams.glb", "garden.glb"];
    const loadedModels = {};
    const draggableObjects = [];

    const loadModel = (file) => {
        return new Promise((resolve, reject) => {
            loader.load(
                `/${file}`,
                (gltf) => {
                    const model = gltf.scene;
                    if (file === "garden.glb") {
                        model.scale.set(1.5, 1.5, 1.5);
                        model.position.set(0, -5, 0);
                    } else {
                        model.scale.set(2, 2, 2);
                    }
                    loadedModels[file] = model;
                    resolve();
                },
                undefined,
                reject
            );
        });
    };

    const placeModel = (fileName, x, z) => {
        const original = loadedModels[fileName];
        if (!original) return;
        const clone = original.clone(true);
        clone.position.set(x, 0, z);
        scene.add(clone);
        draggableObjects.push(clone);
    };

    // OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.1;

    // 드래그 관련
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const plane = new THREE.Plane();
    const intersectPoint = new THREE.Vector3();
    const offset = new THREE.Vector3();
    let selected = null;

    const getIntersects = (event) => {
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        return raycaster.intersectObjects(draggableObjects, true);
    };

    const onMouseDown = (event) => {
        const intersects = getIntersects(event);
        if (intersects.length > 0) {
            selected = intersects[0].object;
            while (selected.parent && !draggableObjects.includes(selected)) {
                selected = selected.parent;
            }
            if (selected) {
                controls.enabled = false;
                const normal = new THREE.Vector3();
                camera.getWorldDirection(normal);
                plane.setFromNormalAndCoplanarPoint(normal, selected.position);
                raycaster.ray.intersectPlane(plane, intersectPoint);
                offset.copy(intersectPoint).sub(selected.position);
            }
        }
    };

    const onMouseMove = (event) => {
        if (!selected) return;
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        raycaster.ray.intersectPlane(plane, intersectPoint);
        selected.position.copy(intersectPoint.sub(offset));
    };

    const onMouseUp = () => {
        selected = null;
        controls.enabled = true;
    };

    renderer.domElement.addEventListener("mousedown", onMouseDown);
    renderer.domElement.addEventListener("mousemove", onMouseMove);
    renderer.domElement.addEventListener("mouseup", onMouseUp);

    Promise.all(files.map(loadModel)).then(() => {
        placeModel("pink-tree.glb", -4, 0);
        placeModel("peng.glb", 0, 0);
        placeModel("hams.glb", 4, 0);
        placeModel("garden.glb", 0, 0);
    });

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };
    animate();
});
</script>
