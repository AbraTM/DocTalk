"use client"

import { useState, useRef, useEffect } from "react"
import Summary from "@/app/components/summary"
import styles from "./MsgBox.module.css"

export default function MsgBox({ currFileId }){
    const [ messages, setMessages ] = useState([])
    const [ input, setInput ] = useState("")
    const [ isLoading, setIsLoading ] = useState(false)
    const msgBoxRef = useRef(null)
    const wsRef = useRef(null)

    useEffect(() => {
        const ws = new WebSocket(`${process.env.NEXT_PUBLIC_BACKEND_WEB_SOCKET_URL}`)
        wsRef.current = ws

        ws.onmessage = (event) => {
            setIsLoading(false)
            setMessages((prev) => [...prev, { sender: "assistant", text: event.data}])
        }

        ws.onerror = (err) => {
            console.error("WebSocket error:", err)
        }

        ws.onclose = () => {
            console.log("WebSocket connection closed")
        }

        return () => ws.close()
    }, [])

    const sendMessage = () => {
        if(!input.trim()) return
        setMessages((prev) => [...prev, { sender: "user", text: input}])
        setIsLoading(true)
        
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(input) 
        } else {
            console.error("WebSocket is not connected")
        }

        setInput("")
    }
    return(
        <div className={styles.chat_main}>
            <div className={styles.scrollable}>
                <Summary currFileId={currFileId}/>
                <h2>Have Questions About This Report?</h2>
                <h2>Ask your medical assistant.</h2>
                <hr></hr>
                <div className={styles.messages}>
                    {messages.map((msg, i) => (
                        <div 
                            key={i}
                            className={`${styles.message} ${msg.sender === "user" ? styles.user : styles.assistant}`}
                        >
                            {msg.text}
                        </div>
                    ))}
                </div>
            </div>
            <div className={styles.msg_box}>
                <textarea 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    ref={msgBoxRef} 
                    type="text" 
                    id="user_msg" 
                    name="user_msg" 
                    placeholder="Ask anything about your report summary."
                    onFocus={() => {
                        if(window.innerWidth <= 768){
                            msgBoxRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center'})
                        } 
                    }}
                />
                <button className={styles.send_btn} onClick={sendMessage}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8.99992 16V6.41407L5.70696 9.70704C5.31643 10.0976 4.68342 10.0976 4.29289 9.70704C3.90237 9.31652 3.90237 8.6835 4.29289 
                        8.29298L9.29289 3.29298L9.36907 3.22462C9.76184 2.90427 10.3408 2.92686 10.707 3.29298L15.707 8.29298L15.7753 8.36915C16.0957 8.76192 
                        16.0731 9.34092 15.707 9.70704C15.3408 10.0732 14.7618 10.0958 14.3691 9.7754L14.2929 9.70704L10.9999 6.41407V16C10.9999 16.5523 
                        10.5522 17 9.99992 17C9.44764 17 8.99992 16.5523 8.99992 16Z"
                        ></path>
                    </svg>
                </button>
            </div>
        </div>
    )
}

            