export const previousChats = async(currFileId) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/file/allFiles`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            file_id: currFileId
        }),
        credentials: "include",
        cache: "no-store"
    })
    if(!res.ok){
        console.log(res)
        return []
    }
    const data = await res.json()
    return data.data
}





