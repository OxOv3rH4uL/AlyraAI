import {Queue} from "bullmq";
import fs from "fs/promises";
import path from "path";


const connection = {
    host:"localhost",
    port:6379
}

const housePlanQueue = new Queue("house-plan-dataset-generation",{
    connection
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main(){


    const folderPath = "C:\\Users\\91994\\OneDrive\\Desktop\\AlyraAI\\backend\\AlyraAIGPT\\normalized_dataset"
    
    const files = await fs.readdir(folderPath)

    for(const file of files){
        const filePath = path.join(folderPath,file)
        const f = await fs.readFile(filePath,"utf-8")
        const housePlan = JSON.parse(f)
    
        const job = await housePlanQueue.add(
            "generate-dataset",
            {
                house_plan:housePlan
            }
        );
    
        console.log("Job addedd successfully!");
        console.log(job.id);
        await sleep(2500);
    }

    await housePlanQueue.close();



}

main();