import styles from "./Footer.module.css";

export default function Footer() {
  return (
    <div className={styles.footer}>
      
      <div className={styles.footerTop}>
        <div className={styles.footerTopLeft}>
          <h2>DocTalk</h2>
          <p>"Understand your health without the jargon."</p>
        </div>
        <p className={styles.disc}>
          *Disclaimer : This tool is for informational purposes only and not a
           substitute for professional medical advice, diagnosis, or treatment.
        </p>
      </div>
      
      <div className={styles.footerLinks}>
        <a href="#" className={styles.footerLink}>Privacy Policy</a>
        <a href="#" className={styles.footerLink}>Terms of Service</a>
        <a href="#" className={styles.footerLink}>Contact Support</a>
      </div>

    </div>
  )
}
