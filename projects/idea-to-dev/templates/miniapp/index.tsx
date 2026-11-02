import { View, Text, Button } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState } from 'react'
import './index.scss'

export default function Index() {
  const [count, setCount] = useState(0)

  return (
    <View className='index'>
      <Text className='title'>欢迎使用应用</Text>
      <Text className='subtitle'>计数: {count}</Text>
      <Button 
        className='btn-primary'
        onClick={() => setCount(count + 1)}
      >
        点击 +1
      </Button>
    </View>
  )
}
