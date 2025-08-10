export const prevMessages = async(currFileId) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/messages`, {
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
    return data
}