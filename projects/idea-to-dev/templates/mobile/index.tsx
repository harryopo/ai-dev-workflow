import { useState } from 'react'
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native'
import { useTodo } from '../shared/todo/hooks/useTodo'
import { MemoryStorageAdapter } from '../shared/todo/storage/memoryStorage'

// Swap to MobileStorageAdapter after installing @react-native-async-storage/async-storage
const storage = new MemoryStorageAdapter()

export default function Home() {
  const { items, addItem, toggleItem, deleteItem } = useTodo(storage)
  const [newItem, setNewItem] = useState('')

  const handleAdd = async () => {
    if (!newItem.trim()) {
      return
    }
    await addItem(newItem)
    setNewItem('')
  }

  const handleDelete = (id: string, name: string) => {
    Alert.alert(
      '确认删除',
      `确定要删除 "${name}" 吗？`,
      [
        { text: '取消', style: 'cancel' },
        {
          text: '删除',
          style: 'destructive',
          onPress: () => deleteItem(id),
        },
      ]
    )
  }

  const renderItem = ({ item }: { item: { id: string; name: string; completed: boolean } }) => (
    <View style={styles.itemContainer}>
      <TouchableOpacity
        style={styles.itemContent}
        onPress={() => toggleItem(item.id)}
      >
        <View style={[
          styles.checkbox,
          !item.completed && styles.checkboxChecked,
        ]}>
          {!item.completed && (
            <Text style={styles.checkmark}>✓</Text>
          )}
        </View>
        <Text style={[
          styles.itemText,
          item.completed && styles.itemTextCompleted,
        ]}>
          {item.name}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.deleteButton}
        onPress={() => handleDelete(item.id, item.name)}
      >
        <Text style={styles.deleteText}>删除</Text>
      </TouchableOpacity>
    </View>
  )

  const completedCount = items.filter((i) => i.completed).length

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>应用名称</Text>
        <Text style={styles.subtitle}>
          共 {items.length} 项 | 已完成 {completedCount} 项 | 待完成 {items.length - completedCount} 项
        </Text>
      </View>

      {/* Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="输入新项目..."
          value={newItem}
          onChangeText={setNewItem}
          onSubmitEditing={handleAdd}
          returnKeyType="done"
        />
        <TouchableOpacity style={styles.addButton} onPress={handleAdd}>
          <Text style={styles.addButtonText}>添加</Text>
        </TouchableOpacity>
      </View>

      {/* List */}
      <FlatList
        data={items}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        style={styles.list}
        contentContainerStyle={items.length === 0 ? styles.emptyContainer : undefined}
        ListEmptyComponent={
          <Text style={styles.emptyText}>暂无数据</Text>
        }
      />
    </KeyboardAvoidingView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    paddingTop: 10,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666666',
    marginTop: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  input: {
    flex: 1,
    height: 44,
    borderWidth: 1,
    borderColor: '#dddddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  addButton: {
    marginLeft: 12,
    backgroundColor: '#1296db',
    borderRadius: 8,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  addButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  list: {
    flex: 1,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#999999',
  },
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    marginHorizontal: 16,
    marginTop: 8,
    borderRadius: 8,
    padding: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  itemContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#dddddd',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  checkboxChecked: {
    backgroundColor: '#4CAF50',
    borderColor: '#4CAF50',
  },
  checkmark: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  itemText: {
    fontSize: 16,
    color: '#333333',
  },
  itemTextCompleted: {
    textDecorationLine: 'line-through',
    color: '#999999',
  },
  deleteButton: {
    padding: 8,
  },
  deleteText: {
    color: '#f44336',
    fontSize: 14,
  },
})
