import React from 'react'
import './TodoList.css'
import { useState } from 'react';
import CreateTodo from './create-todo/CreateTodo';
export const TodoList = ({ todo, handleDelete, handleEdit }) => {
    const [index, setIndex] = useState(null);
    const handleClick = (id) => {
        if (index === todo.id) {
            setIndex(null);
        } else
            setIndex(todo.id);
    };
    return (
        <>
            <div className="todo-item">
                <div className='todo-body'>
                    <div className='todo-texts'>{todo.todo}</div>
                    <div className="todo-status">
                        {todo.is_completed ? "✅" : "❌"}
                    </div>
                    <button className='arrow-button' onClick={handleClick}>⬇️
                    </button>
                    <button className='delete-button' onClick={() => handleDelete(todo.id)}>Delete
                    </button>
                    <button className='delete-button' onClick={() => handleEdit(todo.id)}>Edit
                    </button>
                </div>
                {index === todo.id && (
                    <div className="todo-desc">
                        {todo.description}
                    </div>
                )}
            </div>
        </>
    );
};