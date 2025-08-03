import "./globals.css";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import AuthProvider from "@/context/AuthContext";

export const metadata = {
  title: "DocTalk",
  description: "Simple AI Medical Report Generator",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com"></link>
        <link rel="preconnect" href="https://fonts.gstatic.com" ></link>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap" rel="stylesheet"></link>
      </head>
      <body>
        <AuthProvider>
            <NavBar />
            {children}
            <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
