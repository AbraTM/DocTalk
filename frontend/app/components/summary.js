"use client"

import { useState, useEffect } from "react"
import { currFileSummary } from "@/utils/summary"
import styles from "./summary.module.css"
import Loading from "./Loading"

export default function Summary({ currFileId, onReady }){
    const [ loading, setLoading ] = useState(true)
    const [ summaryData, setSummaryData ] = useState({})
    const [hasCalledReady, setHasCalledReady] = useState(false);
    
    useEffect(() => {
        const getSummaryData = async () => {
            try {
                setLoading(true)
                const summaryRes = await currFileSummary(currFileId)
                setSummaryData(summaryRes)

                if(summaryRes && !hasCalledReady){
                    onReady?.()
                    setHasCalledReady(true)
                }
            } catch (error) {
                console.error("Filed to fetch summary.", error)
            } finally {
                setLoading(false)
            }
        }
        getSummaryData()
    }, [currFileId, onReady, hasCalledReady])
    if(loading){
        return <Loading />
    }
    if(!summaryData){
        return <p>Failed to load summary.</p>
    }
    return(
        <div className={styles.summary}>
            <h2>You're Medical Summary.</h2>
            <hr></hr>
            <div className={styles.summary_l1}>
                <p><b>Level of concern : </b> {summaryData.level_of_concern}</p>
                <p><b>Main Finding : </b> {summaryData.main_finding}</p>
                <hr></hr>
            </div>

            <div className={styles.summary_l2}>
                <p><b>What This Means (In Brief)</b></p>
                <p>{summaryData.quick_summary}</p>
                <hr></hr>
            </div>

            <br></br>
            <div className={styles.summary_l3}>
                <details>
                    <summary><b>Detailed Explaination</b></summary>
                    <p>{summaryData.detailed_summary}</p>
                    <hr></hr>
                </details>
            </div>

            <br></br>
            <br></br>
            <div className={styles.summary_l4}>
                <p><b>Advice</b></p>
                <p>{summaryData.additional_notes}</p>
                <hr></hr>
            </div>

            <br></br>
            <div className={styles.summary_l5}>
                <p><b>Recommended Action</b></p>
                <p>{summaryData.recommended_action}</p>
                <hr></hr>
            </div>
        </div>
    )
}
