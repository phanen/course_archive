package main

type ListNode struct {
    Val int
    Next *ListNode
}
 
func twoSum(a []int, t int) []int {
	m := make(map[int]int)
	for i := 0; i < len(a); i++ {
		k := t - a[i]
		if _, ok := m[k]; ok {
			return []int{m[k], i}
		}
		m[a[i]] = i
	}
	return nil
}

func main() {
 

}

