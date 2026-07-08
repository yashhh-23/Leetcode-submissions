/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode curr = head;
        Stack<ListNode> st = new Stack<>();

        while(curr != null){
            st.push(curr);
            curr = curr.next;
        }
        ListNode reverseHead = new ListNode(-1);
        curr = reverseHead;
        while(!st.isEmpty()){
            curr.next = st.pop();
            curr = curr.next;
            curr.next = null;
        }

        return reverseHead.next;
    }
}

