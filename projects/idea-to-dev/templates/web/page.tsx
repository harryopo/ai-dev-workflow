'use client'

import { useMemo, useState } from 'react'
import { useTodo } from '../shared/todo/hooks/useTodo'
import { WebStorageAdapter } from '../shared/todo/storage/webStorage'

const storage = new WebStorageAdapter()

export default function Home() {
  const { items, addItem, toggleItem, deleteItem } = useTodo(storage)
  const [newItem, setNewItem] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  const filteredItems = useMemo(() => {
    const term = searchTerm.trim().toLowerCase()
    if (!term) {
      return items
    }
    return items.filter((item) => item.name.toLowerCase().includes(term))
  }, [items, searchTerm])

  const handleAdd = async () => {
    if (!newItem.trim()) {
      return
    }
    await addItem(newItem)
    setNewItem('')
  }

  const activeCount = items.filter((item) => !item.completed).length
  const completedCount = items.length - activeCount

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">应用名称</h1>
          <p className="text-gray-600">欢迎使用</p>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="搜索..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Add Item */}
        <div className="flex gap-4 mb-6">
          <input
            type="text"
            placeholder="输入新项目..."
            value={newItem}
            onChange={(e) => setNewItem(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleAdd}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            添加
          </button>
        </div>

        {/* Items List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {filteredItems.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              {items.length === 0 ? '暂无数据' : '没有匹配的结果'}
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredItems.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-4 hover:bg-gray-50">
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() => toggleItem(item.id)}
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                        !item.completed
                          ? 'bg-green-500 border-green-500'
                          : 'border-gray-300'
                      }`}
                    >
                      {!item.completed && (
                        <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </button>
                    <span className={`${
                      item.completed ? 'line-through text-gray-400' : 'text-gray-900'
                    }`}>
                      {item.name}
                    </span>
                  </div>
                  <button
                    onClick={() => deleteItem(item.id)}
                    className="px-3 py-1 text-red-600 hover:bg-red-50 rounded transition-colors"
                  >
                    删除
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="mt-4 text-sm text-gray-500">
          共 {items.length} 项 | 已完成 {completedCount} 项 | 待完成 {activeCount} 项
        </div>
      </div>
    </main>
  )
}
