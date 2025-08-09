import { PuffLoader } from "react-spinners"
import styles from "./Loading.module.css"


export default function Loading(){
    return (
        <div className={styles.loading_cn}>
            <PuffLoader color="gray"/>
        </div>
    )       
}