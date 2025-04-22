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
        0.1,
        1000
    );
    camera.position.set(10, 10, 20);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({
        antialias: true,
        precision: "highp",
    });
    renderer.setSize(window.innerWidth, 600);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.5;
    document
        .getElementById("canvas-container")
        .appendChild(renderer.domElement);

    // 조명
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    scene.add(directionalLight);

    const loader = new GLTFLoader();

    // 세 줄로 배치 (y는 고정, z값만 다르게)
    const files = [
        { name: "hamsterDraco.glb", zOffset: 0 },
        { name: "pinktreeDraco.glb", zOffset: -3 },
        { name: "greentreeDraco.glb", zOffset: -6 },
    ];

    files.forEach(({ name, zOffset }) => {
        for (let i = 0; i < 5; i++) {
            const x = (i - 2) * 2; // 가운데 기준으로 -4, -2, 0, 2, 4 위치
            const z = zOffset;
            loader.load(`/${name}`, (gltf) => {
                const model = gltf.scene;
                model.position.set(x, 0, z);
                model.scale.set(1.5, 1.5, 1.5);
                scene.add(model);
            });
        }
    });

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };

    animate();
});
</script>
