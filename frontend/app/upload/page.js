"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import styles from "./page.module.css"

export default function Upload(){
    const router = useRouter()
    const [ errorMsg, setErrorMsg ] = useState("")
    const handleFileChange = async(event) =>{
        const selectedFile = event.target.files[0]
        if(selectedFile){
            const formData = new FormData()
            formData.append("uploaded_report", selectedFile)
            try{
                const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/file/upload`, {
                    method: "POST",
                    body: formData,
                    credentials: "include"
                })
                const data = await response.json()
                if(response.ok){
                    router.replace(`/chat/${data.file_id}`)
                }
            }catch(error){
                console.error(error)
                setErrorMsg("Something went wrong.")
            } 
        }
        setErrorMsg("")
    }
    return(
        <div className={styles.upload_page}>
            <div className={styles.upload_main}>
                <h2>Upload your report</h2>
                <p>PDF, png, jpg, jpeg</p>
                <form className={styles.upload_img_cn} encType="multipart/form-data">
                    <input 
                        type="file" 
                        id="uploaded_report" 
                        name="uploaded_report" 
                        accept=".pdf,.png,.jpg,.jpeg"
                        onChange={handleFileChange}
                    ></input>
                    <img src="file.png" className={styles.upload_img}></img>
                </form>
                <p
                    className={styles.upload_err}
                    styles={{
                        opacity: errorMsg ? "1" : "0",
                        visibility: errorMsg ? "visible" : "hidden",
                        transition: "opcaity 0.3s ease",
                    }}
                >
                    {errorMsg || ""}
                </p>
            </div>
            <div className={styles.upload_text}>
                <h2 className={styles.upload_head}>Upload Your Medical Report</h2>
                <p>Upload a PDF of your medical test report to get a quick, AI-generated summary. We’ll process your file securely and return insights in plain language — no medical jargon.</p>
            </div>
        </div>
    )
}