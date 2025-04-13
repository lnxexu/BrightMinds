import { ref } from 'vue'
import { supabase } from '@/lib/supabaseClient'

const user = ref(null)

export const useUser = async () => {
  const { data, error } = await supabase.auth.getUser()
  user.value = data?.user || null
  return { user }
}