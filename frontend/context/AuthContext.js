"use client"

import { auth } from "@/utils/firebaseConfig";
import { onAuthStateChanged } from "firebase/auth";
import { useContext, createContext, useState, useEffect } from "react";


const AuthContext = createContext({
    user: null,
    setUser: () => {},
    loading: true,
    setLoading: () => {},
})

const AuthProvider = ({ children }) => {
    console.log(auth)
    const [ user, setUser ] = useState(null)
    const [ loading, setloading ] = useState(true)
    
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async(fb_user) => {
            if(fb_user){
                try {
                    const id_token = await fb_user.getIdToken()
                    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/user/signin`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${id_token}`,
                        },
                    })
                    const result = await response.json()
                    setUser(result)
                    console.log(result)
                } catch (error) {
                    console.error("Error syncing with backend:", error);
                }
            }else{
                setUser(null);
            }
            setloading(false)
        })

        return () => unsubscribe()
    }, [])
    return(
        <AuthContext.Provider value={{ user, setUser, loading, setloading }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthProvider
export const useAuth = () => {
    return useContext(AuthContext)
}