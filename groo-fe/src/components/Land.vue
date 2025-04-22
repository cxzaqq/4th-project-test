<template>
    <canvas ref="renderCanvas" class="canvas-container"></canvas>
  </template>
  
  <script>
  import * as BABYLON from "babylonjs";
  
  export default {
    name: "Land",
    mounted() {
      this.createScene();
    },
    methods: {
      createScene() {
        // 캔버스와 엔진 생성
        const canvas = this.$refs.renderCanvas;
        if (!canvas) {
          console.error("Canvas element not found!");
          return;
        }
  
        const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
  
        // 씬과 카메라 생성
        const scene = new BABYLON.Scene(engine);
        const camera = new BABYLON.ArcRotateCamera(
          "camera",
          Math.PI / 2,
          Math.PI / 4,
          20,
          BABYLON.Vector3.Zero(),
          scene
        );
        camera.attachControl(canvas, true);
  
        // 조명 생성
        const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
  
        // 갈색 땅 재질
        const brownMaterial = new BABYLON.StandardMaterial("brownMaterial", scene);
        brownMaterial.diffuseColor = new BABYLON.Color3(0.6, 0.3, 0); // 갈색
  
        // 연두색 땅 재질
        const greenMaterial = new BABYLON.StandardMaterial("greenMaterial", scene);
        greenMaterial.diffuseColor = new BABYLON.Color3(0.5, 1, 0.5); // 연두색
  
        // 갈색 땅 박스 (두께 1로 설정)
        const brownGround = BABYLON.MeshBuilder.CreateBox("brownGround", { width: 10, height: 1, depth: 10 }, scene);
        brownGround.material = brownMaterial;
        brownGround.position.y = -0.5;  // 땅이 아래로 내려가도록 위치 설정
  
        // 연두색 땅 박스 (두께 0.5로 설정)
        const greenGround = BABYLON.MeshBuilder.CreateBox("greenGround", { width: 10, height: 0.5, depth: 10 }, scene);
        greenGround.material = greenMaterial;
        greenGround.position.y = 0.25;  // 연두색 땅이 위에 배치되도록 위치 설정
  
        // 렌더링 루프
        engine.runRenderLoop(() => {
          scene.render();
        });
  
        // 창 크기 변경 처리
        window.addEventListener("resize", () => {
          engine.resize();
        });
      },
    },
  };
  </script>
  
  <style>
  .canvas-container {
    width: 100%;
    height: 100vh;
    display: block;
  }
  </style>
  