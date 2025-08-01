"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import styles from "./NavBar.module.css";

export default function NavBar() {
    const path = usePathname()
    const isChatPath = path === "/chat"
    const [hamburgMenu, setHamburgMenu] = React.useState(false);
    const [scrolled, setScrolled] = React.useState(false);

    React.useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 10);
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <nav className={styles.mainNav}>
            <div className={`${styles.navTop} ${scrolled ? styles.scrolled : ""}`}>
                <a className={styles.mainLogo}>DocTalk</a>

                <div className={styles.navCenter}>
                    <a>Home</a>
                    <a>Get Started</a>
                    <a>How this works</a>
                </div>

                <button
                    aria-label="Menu"
                    className={styles.navBtn}
                    onClick={() => setHamburgMenu(prev => !prev)}
                >
                    <svg width="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="8" y1="12" x2="29" y2="12" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" />
                        <line x1="8" y1="20" x2="29" y2="20" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" />
                        <line x1="8" y1="28" x2="29" y2="28" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" />
                    </svg>
                </button>
            </div>

            <div className={`${styles.sideNav} ${hamburgMenu ? styles.open : ""}`}>
                <a>Home</a>
                <a>Get Started</a>
                <a>How this works</a>

                <hr></hr>
                <button className={styles.add_new}>
                    <p>Add new report.</p>
                    <span> + </span>
                </button>
                <hr></hr>
                <h3>Previous Reports.</h3>
                <p>Blood Test</p>
                <p>ECG Report</p>
            </div>
        </nav>
    );
}
