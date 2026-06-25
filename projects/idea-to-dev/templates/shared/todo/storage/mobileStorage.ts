import type { TodoItem, TodoStorage } from '../types'

/**
 * React Native TodoStorage implementation backed by AsyncStorage.
 *
 * Dependency required:
 *   npm install @react-native-async-storage/async-storage
 *   or: npx expo install @react-native-async-storage/async-storage
 *
 * If AsyncStorage is not available in the target environment, replace this
 * adapter with a MemoryStorageAdapter or another persistence layer.
 */
export class MobileStorageAdapter implements TodoStorage {
  private async getAsyncStorage() {
    // @ts-expect-error AsyncStorage is an optional peer dependency.
    // Install @react-native-async-storage/async-storage to remove this suppression.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const module: any = await import('@react-native-async-storage/async-storage')
    return module.default as {
      getItem(key: string): Promise<string | null>
      setItem(key: string, value: string): Promise<void>
    }
  }

  private readonly key = 'todo_items'

  async getItems(): Promise<TodoItem[]> {
    try {
      const storage = await this.getAsyncStorage()
      const raw = await storage.getItem(this.key)
      if (!raw) {
        return []
      }
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
    await this._save(items)
    return item
  }

  async updateItem(id: string, updates: Partial<Omit<TodoItem, 'id'>>): Promise<void> {
    const items = await this.getItems()
    const index = items.findIndex((i) => i.id === id)
    if (index === -1) {
      return
    }
    items[index] = { ...items[index], ...updates }
    await this._save(items)
  }

  async deleteItem(id: string): Promise<void> {
    const items = await this.getItems()
    const filtered = items.filter((i) => i.id !== id)
    await this._save(filtered)
  }

  private async _save(items: TodoItem[]): Promise<void> {
    const storage = await this.getAsyncStorage()
    await storage.setItem(this.key, JSON.stringify(items))
  }
}
