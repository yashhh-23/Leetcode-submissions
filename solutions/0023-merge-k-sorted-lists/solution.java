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
    public ListNode mergeKLists(ListNode[] lists) {
        List<ListNode> temp = new ArrayList<>();
        for(ListNode list : lists){
            ListNode curr = list;
            while(curr != null)
            {
                temp.add(curr);
                curr = curr.next;
            }
        }

        Collections.sort(temp, (a, b) -> {
            return a.val - b.val;
        });

        ListNode dummy = new ListNode(-1);
        ListNode curr = dummy;

        for(ListNode node : temp){
            curr.next = node;
            curr = curr.next;
        }

        return dummy.next;
    }
}

