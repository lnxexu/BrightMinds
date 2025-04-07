  import { createClient } from '@supabase/supabase-js'

  const supabaseUrl = 'https://hupwxuuqqwvaoswnhtmi.supabase.co'
  const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1cHd4dXVxcXd2YW9zd25odG1pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI3OTQwMDYsImV4cCI6MjA1ODM3MDAwNn0.M0vi1tjIESPsqKIQuIIOQXSxjdSOXplELsdvYd-Q9MU'
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

// Get user by email and password (for login)
export const getUserByCredentials = async (email) => {
  try {
    const { data, error } = await supabase
      .from('users')
      .select('user_id, full_name, email, created_at')
      .eq('email', email)
      .single()

    if (error) throw error
    return { data, error: null }
  } catch (error) {
    return { data: null, error }
  }
}

// Get user by ID
export const getUserById = async (userId) => {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        user_id,
        full_name,
        email,
        created_at,
        socialaccounts (
          provider,
          unique_id
        )
      `)
      .eq('user_id', userId)
      .single()

    if (error) throw error
    return { data, error: null }
  } catch (error) {
    return { data: null, error }
  }
}

// Get all users with pagination
export const getUsers = async (page = 0, pageSize = 10) => {
  try {
    const from = page * pageSize
    const to = from + pageSize - 1

    const { data, error, count } = await supabase
      .from('users')
      .select('user_id, full_name, email, created_at', { count: 'exact' })
      .range(from, to)
      .order('created_at', { ascending: false })

    if (error) throw error
    return { data, count, error: null }
  } catch (error) {
    return { data: null, count: 0, error }
  }
}

// Check if email exists
export const checkEmailExists = async (email) => {
  try {
    const { data, error, count } = await supabase
      .from('users')
      .select('email', { count: 'exact' })
      .eq('email', email)

    if (error) throw error
    return { exists: count > 0, error: null }
  } catch (error) {
    return { exists: false, error }
  }
}

// Insert a single row into a table
export const insertRow = async (table, data) => {
  try {
    const { data: result, error } = await supabase
      .from(table)
      .insert([data])
      .select()

    if (error) throw error
    return { data: result[0], error: null }
  } catch (error) {
    return { data: null, error }
  }
}

// Insert multiple rows into a table
export const insertRows = async (table, rows) => {
  try {
    const { data: result, error } = await supabase
      .from(table)
      .insert(rows)
      .select()

    if (error) throw error
    return { data: result, error: null }
  } catch (error) {
    return { data: null, error }
  }
}

// Insert or update (upsert) rows in a table
export const upsertRows = async (table, rows, onConflict = 'id') => {
  try {
    const { data: result, error } = await supabase
      .from(table)
      .upsert(rows, { onConflict })
      .select()

    if (error) throw error
    return { data: result, error: null }
  } catch (error) {
    return { data: null, error }
  }
}