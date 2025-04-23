<template>
    <div class="plus">
        <h1>덧셈 기능 만들기</h1>
        <label>num1: </label><input type="text" v-model="num1" />&nbsp;
        <label>num2: </label><input type="text" v-model="num2" />&nbsp;
        <button @click="sendPlus">sendPlus</button>
        <p>{{ num1 }} + {{ num2 }} = {{ sum }}</p>
    </div>
</template>

<script setup>
import { ref } from "vue";

const num1 = ref(0);
const num2 = ref(0);
const sum = ref(0);

const sendPlus = async () => {
    const response = await fetch(
        /* 1. 백엔드에서 CORS 처리를 했을 경우 */
        // `http://localhost:7777/plus?num1=${num1.value}&num2=${num2.value}`

        /* 2. 프론트에서 proxy를 사용해서 우회하는 경우 */
        // `http://localhost:5173/api/plus?num1=${num1.value}&num2=${num2.value}`

        /* 이후 코드는 POST 요청 및 body 활용(백엔드 수정됨) */
        // `http://localhost:5173/api/plus`,
        // {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json;charset=utf-8",
        //     },
        //     body: JSON.stringify({ num1: num1.value, num2: num2.value }),
        // },

        /* 3. 백엔드에서 cors, 프론트에서 X (백, 프론트 둘 다 컨테이너화 이후) */
        // `http://localhost:8055/plus`,
        // {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json;charset=utf-8",
        //     },
        //     body: JSON.stringify({ num1: num1.value, num2: num2.value }),
        // }

        /* 4. 백엔드에서 x, 프론트에서 cors(docker compose를 활용해 네트워크로 통신, 둘 다 컨테이너) */
        // `http://localhost:8011/api/plus`,
        // {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json;charset=utf-8",
        //     },
        //     body: JSON.stringify({ num1: num1.value, num2: num2.value }),
        // }

        // /* 5. 백엔드에서 cors, 프론트에서 x(kubernetes의 백엔드 워커노드로 요청) */
        // `http://localhost:30001/plus`,
        // {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json;charset=utf-8",
        //     },
        //     body: JSON.stringify({ num1: num1.value, num2: num2.value }),
        // }

        /* 6. 백, 프론트 X (kubernetes의 ingress 추가 후후) */
        `/boot/plus`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify({ num1: num1.value, num2: num2.value }),
        }
    );
    const data = await response.json();
    sum.value = data.sum;
    console.log("data:", data);
};
</script>

<style scoped></style>
