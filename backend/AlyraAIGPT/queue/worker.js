import {Worker} from "bullmq"
import { redisConnection } from "./connection.js"
import fs from "fs/promises";
import path from "path";

const output_path = "C:\\Users\\91994\\OneDrive\\Desktop\\AlyraAI\\backend\\AlyraAIGPT\\ai_dataset"
const connection = {
    host:"localhost",
    port:6379
}

const worker = new Worker(
    "house-plan-dataset-generation",
    async(job)=>{
        console.log("Received job:", job.id);
        const housePlan = job.data.house_plan

        const response = await fetch("http://127.0.0.1:7777/generate",{
            method: "POST",
            headers:{
                "Content-Type" : "application/json"
            },
            body: JSON.stringify({
                house_plan:housePlan
            })
        })

        if(!response.ok){
            throw new Error(
                response.status
            )
        }
        const result = await response.json()
        const training_data = {
            request: result.request,
            house_plan : housePlan
        }
        await fs.writeFile(
            path.join(output_path, `${job.id}.json`),
            JSON.stringify(training_data, null, 2)
        );

        console.log(
            `${job.id} training data saved successfully!!`
        );
    },
    {
        connection
    }
);

worker.on("completed", (job) => {
    console.log(`Job ${job.id} completed`);
});

worker.on("failed", (job, error) => {
    console.error(`Job ${job.id} failed:`, error);
});

console.log("Worker is running...");