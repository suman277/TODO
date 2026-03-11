import React from 'react'
import "./ActivityList.css"

const ActivityList = ({ log, isLast}) => {
    const {changes_json} = log
    return (
        <>
            <div className='body'>
                <div className='design-part'>
                    <div className='circle'></div>
                    {!isLast && <div className="straight"></div>}
                    {console.log("Kuch to hua hai")}
                </div>
                <div className='text'>
                    <div>{changes_json}</div>
                </div>
            </div>
        </>
    )
}

export default ActivityList