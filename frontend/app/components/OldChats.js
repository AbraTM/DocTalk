"use client"

import { useState, useEffect } from "react";
import { previousChats } from "@/utils/previousChats";
import styles from "./OldChats.module.css"

export default function OldChats({ currFileId }) {
  const [ oldChats, setOldChats] = useState(null)

  useEffect(() => {
    const getOldChats = async() => {
      const oldChatsRes = await previousChats(currFileId)
      setOldChats(oldChatsRes)
    }
    getOldChats()
  }, [currFileId])
  return (
    <>
      {oldChats && oldChats.map((chat, index) => (
        <a key={index} className={styles.oldchat_item}>{chat.title}</a>
      ))}
    </>
  );
}
