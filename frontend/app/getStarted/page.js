import styles from "./page.module.css";
import SignUpForm from "../components/SignUpForm";

export default function GetStartedPage() {
  return (
    <div className={styles.getStarted}>
      <div className={styles.getStartedLeft}>
      </div>
      <SignUpForm />
    </div>
  )
}
