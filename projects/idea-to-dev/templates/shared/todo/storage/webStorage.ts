import type { TodoItem, TodoStorage } from '../types'

const STORAGE_KEY = 'todo_items'

/**
 * Browser-based TodoStorage implementation backed by localStorage.
 * Safe for Next.js 'use client' pages because reads/writes happen after mount.
 */
export class WebStorageAdapter implements TodoStorage {
  async getItems(): Promise<TodoItem[]> {
    if (typeof window === 'undefined') {
      return []
    }
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return []
    }
    try {
      const parsed = JSON.parse(raw) as TodoItem[]
      return Array.isArray(parsed) ? parsed : []
    } catch {
      return []
    }
  }

  async addItem(name: string): Promise<TodoItem> {
    const items = await this.getItems()
    const item: TodoItem = {
      id: `${Date.now()}`,
      name,
      completed: false,
    }
    items.push(item)
    this._save(items)
    return item
  }

  async updateItem(id: string, updates: Partial<Omit<TodoItem, 'id'>>): Promise<void> {
    const items = await this.getItems()
    const index = items.findIndex((i) => i.id === id)
    if (index === -1) {
      return
    }
    items[index] = { ...items[index], ...updates }
    this._save(items)
  }

  async deleteItem(id: string): Promise<void> {
    const items = await this.getItems()
    const filtered = items.filter((i) => i.id !== id)
    this._save(filtered)
  }

  private _save(items: TodoItem[]): void {
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
    }
  }
}
