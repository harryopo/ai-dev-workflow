import { NextResponse } from 'next/server'

// GET 请求处理
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  
  // TODO: 从数据库获取数据
  const data = {
    message: 'Hello',
    id: id || 'none'
  }
  
  return NextResponse.json(data)
}

// POST 请求处理
export async function POST(request: Request) {
  try {
    const body = await request.json()
    
    // TODO: 处理业务逻辑，保存到数据库
    
    return NextResponse.json({ 
      success: true, 
      message: '创建成功',
      data: body 
    })
  } catch (error) {
    return NextResponse.json(
      { success: false, message: '请求格式错误' },
      { status: 400 }
    )
  }
}

// PUT 请求处理
export async function PUT(request: Request) {
  try {
    const body = await request.json()
    
    // TODO: 更新数据库
    
    return NextResponse.json({ 
      success: true, 
      message: '更新成功' 
    })
  } catch (error) {
    return NextResponse.json(
      { success: false, message: '请求格式错误' },
      { status: 400 }
    )
  }
}

// DELETE 请求处理
export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  
  if (!id) {
    return NextResponse.json(
      { success: false, message: '缺少 id 参数' },
      { status: 400 }
    )
  }
  
  // TODO: 从数据库删除
  
  return NextResponse.json({ 
    success: true, 
    message: '删除成功' 
  })
}
