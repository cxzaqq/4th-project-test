<template>
    <div id="babylon-canvas-container"></div>
</template>

<script setup>
import { onMounted } from "vue";
import * as BABYLON from "babylonjs";
import "babylonjs-loaders"; // .glb 파일을 로드할 때 필요

onMounted(() => {
    const canvas = document.createElement("canvas");
    const container = document.getElementById("babylon-canvas-container");
    container.appendChild(canvas);

    // 엔진 초기화
    const engine = new BABYLON.Engine(canvas, true);

    // 윈도우 크기에 맞춰 캔버스 크기 설정
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const scene = new BABYLON.Scene(engine);

    // 카메라 생성
    const camera = new BABYLON.ArcRotateCamera(
        "camera1",
        Math.PI / 2,
        Math.PI / 2,
        50, // 초기 각도와 거리
        BABYLON.Vector3.Zero(), // 카메라가 바라볼 위치 (중앙)
        scene
    );
    camera.attachControl(canvas, true);

    // 라이트 추가
    const light = new BABYLON.HemisphericLight(
        "light1",
        BABYLON.Vector3.Up(),
        scene
    );

    // .glb 파일 로드
    BABYLON.SceneLoader.Append(
        "/", // 모델이 위치한 경로
        "forest_background.glb", // 모델 파일명
        scene, // 장면
        function () {
            console.log("배경 모델 로딩 완료!");
        },
        function (scene, message) {
            console.error("모델 로딩 실패: " + message);
        }
    );

    // 블러 효과 추가
    scene.onReadyObservable.add(() => {
        // 카메라에 블러 포스트 프로세스 추가
        const blurPostProcess = new BABYLON.BlurPostProcess(
            "blur", // 효과 이름
            1.0, // 블러 강도
            camera, // 카메라
            BABYLON.Texture.BILINEAR_SAMPLINGMODE, // 텍스처 샘플링 모드
            scene, // 장면
            true // 활성화
        );
    });

    // 애니메이션 루프
    engine.runRenderLoop(() => {
        scene.render();
    });

    // 윈도우 리사이징 처리
    window.addEventListener("resize", () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        engine.resize(); // 엔진 크기 조정
    });
});
</script>

<style scoped>
#babylon-canvas-container {
    width: 100vw;
    height: 100vh;
    position: relative;
}

canvas {
    width: 100%;
    height: 100%;
    display: block;
}
</style>
