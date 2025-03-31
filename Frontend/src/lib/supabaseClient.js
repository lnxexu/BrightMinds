import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://hupwxuuqqwvaoswnhtmi.supabase.co'
const supabaseKey = process.env.SUPABASE_KEY
export const supabase = createClient(supabaseUrl, supabaseKey)

// Get all courses with optional column selection
export const getCourses = async (columns = '*') => {
  const { data, error } = await supabase
    .from('courses')
    .select(columns)

  return { data, error }
}

// Example: Get courses with specific columns and relationships
export const getCoursesWithDetails = async () => {
  const { data, error } = await supabase
    .from('courses')
    .select(`
      id,
      title,
      description,
      created_at,
      users (
        id,
        email
      )
    `)

  return { data, error }
}