<template>
    <div id="canvas-container" style="width: 100vw; height: 100vh"></div>
</template>

<script setup>
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { DRACOLoader } from "three/examples/jsm/loaders/DRACOLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { DragControls } from "three/examples/jsm/controls/DragControls";
import { onMounted } from "vue";

onMounted(() => {
    const scene = new THREE.Scene();

    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 40;
    const camera = new THREE.OrthographicCamera(
        (frustumSize * aspect) / -2,
        (frustumSize * aspect) / 2,
        frustumSize / 2,
        frustumSize / -2,
        1,
        1000
    );

    // ✅ 아이소메트릭 시점 느낌
    camera.position.set(0, 50, 40);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document
        .getElementById("canvas-container")
        .appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(10, 20, 10);
    scene.add(directionalLight);

    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath("/draco/");
    const loader = new GLTFLoader();
    loader.setDRACOLoader(dracoLoader);

    // ✅ 배경 설정
    loader.load("/forest_background.glb", (gltf) => {
        const background = gltf.scene;
        background.scale.set(15, 15, 15);
        // 배경 모델의 크기를 기준으로 위치 조정
        const backgroundSize = 15 * 15; // scale factor (배경 크기)
        background.position.set(-20, -backgroundSize / 2, -30); // 배경을 화면 중앙에 위치시킴

        scene.add(background);
    });

    const draggableObjects = [];
    const files = [
        { name: "pinktreeDraco.glb", xOffset: -10 },
        { name: "greentreeDraco.glb", xOffset: -5 },
        { name: "hamsterDraco.glb", xOffset: 0 },
        { name: "penguine.glb", xOffset: 5 },
    ];

    files.forEach(({ name, xOffset }) => {
        for (let i = 0; i < 2; i++) {
            const x = xOffset + i * 4;
            const y = 0; // 평지 위
            const z = i * 5;

            loader.load(
                `/${name}`,
                (gltf) => {
                    const model = gltf.scene;
                    model.position.set(x, y, z);
                    model.scale.set(25, 25, 25);

                    // 👇 여기 추가!
                    model.rotation.y = -Math.PI / 2;

                    scene.add(model);
                    draggableObjects.push(model);
                },
                undefined,
                (error) => {
                    console.error(`❌ 모델 로딩 실패: ${name}`, error);
                }
            );
        }
    });

    // ✅ 카메라 컨트롤
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enablePan = true;
    controls.enableRotate = false;
    controls.enableZoom = true;

    // ✅ 드래그 컨트롤
    let dragControls;
    setTimeout(() => {
        dragControls = new DragControls(
            draggableObjects,
            camera,
            renderer.domElement
        );

        dragControls.addEventListener("dragstart", () => {
            controls.enabled = false;
        });

        dragControls.addEventListener("dragend", () => {
            controls.enabled = true;
        });

        dragControls.addEventListener("drag", (event) => {
            const obj = event.object;
            obj.position.y = 0; // y축 고정 (날지 않게)
        });
    }, 1000);

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };

    animate();
});
</script>
