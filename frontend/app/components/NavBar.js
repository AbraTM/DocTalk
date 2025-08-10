"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import styles from "./NavBar.module.css";
import { logout } from '@/utils/firebaseAuth';
import OldChats from './OldChats';

export default function NavBar() {
    const path = usePathname()
    const isChatPath = path.split("/")[1] === "chat"
    const currFileId = path.split("/")[2]
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
                <a href='/' className={styles.mainLogo}>DocTalk</a>

                <div className={styles.navCenter}>
                    <a href='/'>Home</a>
                    <a href='/getStarted'>Get Started</a>
                    <a href='/'>How this works</a>
                </div>
                <button className={styles.logout_nav} onClick={logout}>Logout</button>
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
                <a href='/'>Home</a>
                <a href='/getStarted'>Get Started</a>
                <a href='/'>How this works</a>

                <hr></hr>
                {
                    isChatPath
                    &&
                    <div>
                        <a href="/upload" className={styles.add_new}>
                            <p>Add new report.</p>
                            <span> + </span>
                        </a>
                        <hr></hr>
                        <h3>Previous Reports.</h3>
                        <OldChats currFileId={currFileId}/>
                    </div>
                }
                <button className={styles.logout_ham} onClick={logout}>Logout</button>
            </div>
        </nav>
    );
}
