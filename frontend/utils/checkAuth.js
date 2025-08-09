import { cookies } from "next/headers";

export async function checkAuth(){
    const cookieStore = cookies()
    const token = cookieStore.get("accessToken")?.value

    if(!token){
        return false;
    }

    try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/user/verify`, {
            cache: 'no-store'
        })
        const data = await res.json()
        console.log(data)
        
        if(!res.ok){
            return false;
        } 
        
        return true;
    } catch (error) {
        return false;
    }
}