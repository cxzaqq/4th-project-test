<template>
    <div ref="sceneContainer" class="w-full h-screen"></div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import * as THREE from 'three'
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
  
  const sceneContainer = ref(null)
  
  onMounted(() => {
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xd7f5e9)
  
    const camera = new THREE.OrthographicCamera(
      window.innerWidth / -20,
      window.innerWidth / 20,
      window.innerHeight / 20,
      window.innerHeight / -20,
      1,
      1000
    )
    camera.position.set(100, 100, 100)
    camera.lookAt(0, 0, 0)
  
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(window.innerWidth, window.innerHeight)
    sceneContainer.value.appendChild(renderer.domElement)
  
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8)
    scene.add(ambientLight)
  
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6)
    directionalLight.position.set(50, 100, 50)
    scene.add(directionalLight)
  
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(200, 200),
      new THREE.MeshStandardMaterial({ color: 0xc0eac0 })
    )
    ground.rotation.x = -Math.PI / 2
    scene.add(ground)
  
    const loader = new GLTFLoader()
    const itemPositions = [
      [0, 0], [10, -10], [-15, 5], [20, 15], [-20, -15],
      [5, 20], [-25, -5], [15, -20], [0, 25], [-10, -25]
    ]
  
    loader.load('/models/tree.glb', (gltf) => {
      itemPositions.forEach(([x, z]) => {
        const model = gltf.scene.clone()
        model.position.set(x, 0, z)
        model.scale.set(3, 3, 3)
        scene.add(model)
      })
    })
  
    const animate = () => {
      requestAnimationFrame(animate)
      renderer.render(scene, camera)
    }
    animate()
  })
  </script>
  
  <style scoped>
  div {
    overflow: hidden;
  }
  </style>
  