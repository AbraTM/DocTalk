import styles from "./summary.module.css"

const data = {
  "level_of_concern": "Moderate",
  "main_finding": "Mild anemia detected (Hemoglobin: 10.8 g/dL)",
  "quick_summary": "Your blood test shows a mildly low hemoglobin level, which may indicate anemia. This is not urgent but should be followed up with your doctor.",
  "detailed_summary": "Your complete blood count (CBC) shows a hemoglobin level of 10.8 g/dL, which is slightly below the normal reference range (typically 12–16 g/dL for adult females, 13–17 g/dL for adult males). Hemoglobin helps carry oxygen in the blood, and low levels may cause fatigue, weakness, or shortness of breath. Your red blood cell count and hematocrit are also mildly decreased, supporting the presence of anemia. White blood cell and platelet counts are within normal limits, which suggests no signs of active infection or bleeding. This type of mild anemia may be caused by iron deficiency, dietary issues, or chronic low-level blood loss (e.g., heavy menstruation, ulcers). It is not immediately dangerous but warrants further evaluation, especially if you are experiencing symptoms. Your doctor may recommend iron studies, dietary adjustments, or additional testing depending on your history. Regular monitoring may also be advised.",
  "additional_notes": "Speak with your primary care provider about these results. Consider scheduling follow-up blood tests to determine the cause of anemia. Increase iron-rich foods in your diet such as leafy greens, beans, or red meat. Avoid taking iron supplements unless directed by a healthcare provider.",
  "tags": ["anemia", "hemoglobin", "CBC", "iron deficiency", "fatigue"],
  "recommended_action": "Consult Doctor"
}


export default function Summary(){
    return(
        <div className={styles.summary}>
            <h2>You're Medical Summary.</h2>
            <hr></hr>
            <div className={styles.summary_l1}>
                <p><b>Level of concern : </b> {data.level_of_concern}</p>
                <p><b>Main Finding : </b> {data.main_finding}</p>
                <hr></hr>
            </div>

            <div className={styles.summary_l2}>
                <p><b>What This Means (In Brief)</b></p>
                <p>{data.quick_summary}</p>
                <hr></hr>
            </div>

            <br></br>
            <div className={styles.summary_l3}>
                {/* <p><b>Detailed Explaination</b></p>
                <p>{data.detailed_summary}</p>
                <hr></hr> */}
                <details>
                    <summary><b>Detailed Explaination</b></summary>
                    <p>{data.detailed_summary}</p>
                    <hr></hr>
                </details>
            </div>

            <br></br>
            <br></br>
            <div className={styles.summary_l4}>
                <p><b>Advice</b></p>
                <p>{data.additional_notes}</p>
                <hr></hr>
            </div>

            <br></br>
            <div className={styles.summary_l5}>
                <p><b>Recommended Action</b></p>
                <p>{data.recommended_action}</p>
                <hr></hr>
            </div>
        </div>
    )
}