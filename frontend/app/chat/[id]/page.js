import styles from "./page.module.css"
import OldChats from "@/app/components/OldChats"
import MsgBox from "@/app/components/MsgBox"

export default async function ChatPage({ params }){
    const { id } = await params
    const currFileId = id
    return(
        <div className={styles.chat_page}>
            <div className={styles.side_bar}>
                <button className={styles.add_new}>
                    <p>Add new report.</p>
                    <span> + </span>
                </button>
                <hr></hr>
                <h3>Previous Reports.</h3>
                <OldChats currFileId={currFileId}/>
            </div>
            <MsgBox currFileId={currFileId}/>
        </div>
    )
}
