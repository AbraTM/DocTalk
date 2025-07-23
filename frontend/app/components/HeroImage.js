"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import styles from "./HeroImage.module.css";

export default function HeroImage() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start", "250px"],
  });

  const width = useTransform(scrollYProgress, [0, 1], ["120%", "80%"]);
  const borderRadius = useTransform(scrollYProgress, [0, 1], ["0px", "30px"]);

  return (
    <div style={{ overflow: "hidden", display: "flex", justifyContent: "center" }}>
      <motion.div
        ref={ref}
        style={{
          width,
          height: "120vh",
          backgroundImage: 'url(/man.jpg)',
          backgroundSize: "cover",
          borderRadius,
        }}
        className={styles.heroImg}
      />
    </div>
  );
}
