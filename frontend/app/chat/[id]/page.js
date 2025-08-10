import styles from "./page.module.css"
import OldChats from "@/app/components/OldChats"
import MsgBox from "@/app/components/MsgBox"
import { cookies } from "next/headers"

export default async function ChatPage({ params }){
    const cookieStore = await cookies()
    const { id } = await params
    const currFileId = id
    const userAccessToken = cookieStore.get("accessToken").value
    return(
        <div className={styles.chat_page}>
            <div className={styles.side_bar}>
                <a href="/upload" className={styles.add_new}>
                    <p>Add new report.</p>
                    <span> + </span>
                </a>
                <hr></hr>
                <h3>Previous Reports.</h3>
                <OldChats currFileId={currFileId}/>
            </div>
            <MsgBox currFileId={currFileId} token={userAccessToken}/>
        </div>
    )
}
