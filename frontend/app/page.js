import Link from 'next/link';
import styles from "./page.module.css";
import HeroImage from "./components/HeroImage";


export default async function HomePage(){
  return(
    <div className={styles.home}>
      <div className={styles.heroTop}>
        <p>
          No more Googling medical jargon. Just upload your
           report — we’ll handle the rest.
        </p>

        <button className={styles.getStarted}>
          <Link href="/getStarted">Get Started</Link>
        </button>
      </div>

      <HeroImage />
    </div>
  )  
}