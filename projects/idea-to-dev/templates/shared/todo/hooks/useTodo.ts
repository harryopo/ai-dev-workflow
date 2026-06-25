import { useCallback, useEffect, useMemo, useState } from 'react'
import { TodoService } from '../todoService'
import type { TodoItem, TodoStats, TodoStorage } from '../types'

export interface UseTodoResult {
  items: TodoItem[]
  isLoading: boolean
  error: string | null
  stats: TodoStats
  addItem: (name: string) => Promise<void>
  toggleItem: (id: string) => Promise<void>
  deleteItem: (id: string) => Promise<void>
  refresh: () => Promise<void>
}

/**
 * Shared React hook for Todo state management.
 * Works in both React DOM (Web) and React Native (Mobile) because it only
 * depends on a TodoStorage adapter, not on any platform-specific API.
 */
export function useTodo(storage: TodoStorage): UseTodoResult {
  const [service] = useState(() => new TodoService(storage))
  const [items, setItems] = useState<TodoItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    try {
      setError(null)
      const loaded = await service.getItems()
      setItems(loaded)
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载失败')
    }
  }, [service])

  useEffect(() => {
    let mounted = true
    setIsLoading(true)
    service
      .getItems()
      .then((loaded) => {
        if (mounted) {
          setItems(loaded)
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err instanceof Error ? err.message : '加载失败')
        }
      })
      .finally(() => {
        if (mounted) {
          setIsLoading(false)
        }
      })
    return () => {
      mounted = false
    }
  }, [service])

  const addItem = useCallback(
    async (name: string) => {
      try {
        setError(null)
        await service.addItem(name)
        await refresh()
      } catch (err) {
        setError(err instanceof Error ? err.message : '添加失败')
        throw err
      }
    },
    [service, refresh]
  )

  const toggleItem = useCallback(
    async (id: string) => {
      try {
        setError(null)
        await service.toggleItem(id)
        await refresh()
      } catch (err) {
        setError(err instanceof Error ? err.message : '更新失败')
      }
    },
    [service, refresh]
  )

  const deleteItem = useCallback(
    async (id: string) => {
      try {
        setError(null)
        await service.deleteItem(id)
        await refresh()
      } catch (err) {
        setError(err instanceof Error ? err.message : '删除失败')
      }
    },
    [service, refresh]
  )

  const stats = useMemo(() => service.getStats(items), [service, items])

  return {
    items,
    isLoading,
    error,
    stats,
    addItem,
    toggleItem,
    deleteItem,
    refresh,
  }
}
