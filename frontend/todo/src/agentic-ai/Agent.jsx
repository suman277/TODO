import React, { useState, useRef, useEffect } from "react";
import "./Agent.css"
import { useNavigate } from "react-router-dom";

const Agent = () => {
    const naviagate = useNavigate()
    const [message, setMessage] = useState([]);
    const [loading, setLoading] = useState(false)
    const [sessionId, setSessionId] = useState("")
    const inputMessage = useRef(null)
    const token = localStorage.getItem("token")
    const handleNavigate = () =>{
        naviagate(-1);
    }

    async function* streamSseEvents(responseBody) {
        const reader = responseBody.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            buffer = buffer.replace(/\r\n/g, "\n");

            let boundary;
            while ((boundary = buffer.indexOf("\n\n")) !== -1) {
                const chunk = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + 2);

                if (!chunk.startsWith("data:")) continue;

                const payload = chunk.slice(5).trim();
                if (!payload) continue;

                yield JSON.parse(payload);
            }
        }
    }

    // const handleSendMessage = async (agentStateSessionId, overrideMsg) => {
    //     const userText = overrideMsg || inputMessage?.current?.value.trim()
    //     const message = {
    //         id: Date.now(),
    //         type: "message",
    //         sender: "user",
    //         text: userText,
    //     }
    //     if (!userText || !agentStateSessionId || loading) {
    //         return
    //     }
    //     const buildMessage = []
    //     buildMessage.push({ "text": userText });
    //     const payload = {
    //         appName: "agents",
    //         sessionId: agentStateSessionId,
    //         stateDelta: null,
    //         streaming: false,
    //         userId: "user",
    //         newMessage: { role: "user", parts: buildMessage }
    //     }
    //     setMessage((prev => [...prev, message]));
    //     const response = await fetch("http://127.0.0.1:8001/run_sse", {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify(payload),
    //     })
    //     if (!response.ok) {
    //         const error = await response.json();
    //         const message = {
    //             id: Date.now(),
    //             type: "error",
    //             sender: "model",
    //             text: error.message || "Something Went wrong"
    //         }
    //         setMessage((prev) => [
    //             ...prev,
    //             message
    //         ])
    //     }
    //     const data = await response.json()
    //     data?.contents?.parts?.forEach((part) => {
    //         if (part.text) {
    //             const message = {
    //                 id: Date.now(),
    //                 type: "message",
    //                 sender: "model",
    //                 text: part.text
    //             }
    //             setMessage((prev) => [
    //                 ...prev,
    //                 message
    //             ])
    //         }
    //     })
    // }

    const handleSendMessage = async (agentStateSessionId, overrideMsg) => {
        const userText = overrideMsg || inputMessage?.current?.value.trim()
        const message = {
            id: Date.now(),
            type: "message",
            sender: "user",
            text: userText,
        }

        if (!userText || !agentStateSessionId || loading) {
            return
        }

        const buildMessage = []
        buildMessage.push({ text: userText });

        const payload = {
            appName: "agents",
            sessionId: agentStateSessionId,
            stateDelta: null,
            streaming: true, // 🔥 ONLY CHANGE
            userId: "user",
            newMessage: { role: "user", parts: buildMessage }
        }

        setMessage((prev => [...prev, message]));

        const response = await fetch("http://127.0.0.1:8001/run_sse", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
                Accept: "text/event-stream" // 🔥 ONLY CHANGE
            },
            body: JSON.stringify(payload),
        })

        if (!response.ok || !response.body) {
            const error = await response.json();
            setMessage((prev) => [
                ...prev,
                {
                    id: Date.now(),
                    type: "error",
                    sender: "model",
                    text: error.message || "Something Went wrong"
                }
            ])
            return;
            setMessage([])
        }

        // 🔥 STREAM READER (ADDED, NOT REFACTORED)
        for await (const data of streamSseEvents(response.body)) {
            data?.content?.parts?.forEach((part) => {
                if (!part.text) return;

                setMessage((prev) => {
                    const last = prev[prev.length - 1];

                    // continue streaming message
                    if (last?.sender === "model" && last.streaming) {
                        return prev.map((msg) =>
                            msg.id === last.id
                                ? { ...msg, text: msg.text + part.text }
                                : msg
                        );
                    }

                    // start new streaming message
                    return [
                        ...prev,
                        {
                            id: data.id || Date.now(),
                            type: "message",
                            sender: "model",
                            text: part.text,
                            streaming: true
                        }
                    ];
                });
            });

            // finalize message
            if (data.partial === false) {
                setMessage((prev) =>
                    prev.map((msg) =>
                        msg.streaming ? { ...msg, streaming: false } : msg
                    )
                );
            }
        }
    }

    const createNewSession = async () => {
        console.log("create new session is called");
        setLoading(true)
        try {
            const response = await fetch("http://127.0.0.1:8001/apps/agents/users/user/sessions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({})
            });
            if (!response.ok) throw new Error("An internal Error Occured");
            console.log("got fucked");
            const data = await response.json()
            setMessage([])
            setSessionId(data.id);
            sessionStorage.setItem("agentConfig", JSON.stringify({ agentSessionToken: data.id }));
            setLoading(false);
        }
        catch (error) {
            const errMessage = error instanceof Error ? error.message : "An error Occured"
            setMessage((prev) => [
                ...prev,
                {
                    id: Date.now(),
                    type: "error",
                    sender: "model",
                    text: "Failed to start a session"
                }
            ])
        }
    }

    useEffect(() => {
        const loadSessionMessages = async (sessionId) => {
            try {
                const response = await fetch(`http://127.0.0.1:8001/apps/agents/users/user/sessions/${sessionId}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        }
                    }
                )
                if (!response.ok) {
                    throw new Error("An Error Occured");
                }
                const data = await response.json()
                const messageMap = new Map()
                data.events.forEach((event) => {
                    const { content, id, timestamp } = event;
                    content?.parts?.forEach((part) => {
                        if (part.text) {
                            messageMap.set(id, {
                                id,
                                type: "message",
                                sender: content.role === "user" ? "user" : "model",
                                text: part.text
                            })
                        }

                    })
                })
                setMessage(Array.from(messageMap.values()))
            }

            catch (err) {
                console.error("An error occured");
            }
            finally {
                setLoading(false)
            }
        }
        const agentConfig = JSON.parse(sessionStorage.getItem("agentConfig"))
        if (agentConfig?.agentSessionToken) {
            setSessionId(agentConfig.agentSessionToken);
            loadSessionMessages(agentConfig.agentSessionToken);
        } else {
            createNewSession();
        }
    }, [])
    return (
        <>
            <div className="full-body">
                <div className="navbar">
                    <div className="return">
                        <button className="back-button" onClick={handleNavigate}>Back</button>
                    </div>
                    <div className="bot-wrapper">
                        <div className="agent-icon"> :) </div>
                        <span>Todo Assistant Agent</span>
                    </div>
                    <div className="session-button">
                        <button className="session-btn" onClick={createNewSession}>New Session</button>
                    </div>
                </div>
                <div className="body-wrapper">
                    {message.map(msg => (
                        <div
                            key={msg.id}
                            className={msg.sender === "user" ? "msgRow right" : "msgRow left"}
                        >
                            <div className="bubble">{msg.text}</div>
                        </div>
                    ))}
                </div>
                <div className="input-wrapper">
                    <input className="message" placeholder="Start the conversation here..." ref={inputMessage}></input>
                    <button className="btn-send" onClick={() => { handleSendMessage(sessionId) }}>Send</button>
                </div>
            </div>
        </>
    )
}

export default Agent;