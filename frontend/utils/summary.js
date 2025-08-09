export const currFileSummary = async(currFileId) => {
    while(true){
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/summary/getSummary`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                file_id: currFileId
            }),
            credentials: "include",
            cache: "no-store"
        })
        const data = await res.json()
        if(data.status === "ready"){
            return data.data
        }

        console.log("Summary still processing...")
        await new Promise((resolve) => setTimeout(resolve, 5000))
    }
}