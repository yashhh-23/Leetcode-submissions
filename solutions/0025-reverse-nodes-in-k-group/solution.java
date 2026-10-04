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
    public ListNode reverseKGroup(ListNode head, int k) {
        int count = 0;
        ListNode dummy = new ListNode(-1);
        dummy.next=head;
        ListNode being = dummy;
        while(head!=null)
        {
            count++;
            if(count%k==0)
            {
                being = reverse(being, head.next);
                head=being.next;
            } else
            {
                head=head.next;
            }
        } return dummy.next;
    } 
    private ListNode reverse(ListNode being, ListNode end)
    {
        ListNode prev = being;
        ListNode curr=being.next;
        ListNode fast = curr.next;
        ListNode first= being.next;
        while(fast!=end)
        {
            curr.next=prev;
            prev=curr;
            curr=fast;
fast=fast.next;
        } curr.next=prev;
        being.next=curr;
        first.next=end;
return first;
    }
}
