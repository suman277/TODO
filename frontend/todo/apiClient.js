import { useEffect, useState } from "react";


export const useGetAPI = (endpoint) => {
    const [datas, setData] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!endpoint) return;

        const token = localStorage.getItem("token");
        const controller = new AbortController();

        setLoading(true);
        setError("");

        fetch(`http://localhost:8000/${endpoint}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                ...(token && { Authorization: `Bearer ${token}` }),
            },
            signal: controller.signal,
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}`);
                }
                return res.json();
            })
            .then((result) => {
                const extractedData =
                    Array.isArray(result) ? result :
                        Array.isArray(result?.data) ? result.data :
                            Array.isArray(result?.data?.data) ? result.data.data :
                                [];
                setData(extractedData);
            })
            .catch((err) => {
                if (err.name !== "AbortError") {
                    setError(err.message);
                }
            })
            .finally(() => {
                setLoading(false);
            });

        return () => controller.abort();
    }, [endpoint]);

    return { datas, error, loading };
};

export default useGetAPI;