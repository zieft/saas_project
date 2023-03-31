# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    @staticmethod
    def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
        # 初始化个位节点，先不做进位
        newPoint = ListNode(l1.val + l2.val)

        # tp用来遍历节点
        tp = newPoint

        # l1,l2只要后面还有节点，就继续往后遍历；或者新链表还需要继续往后进位
        while (l1 and l1.next) or (l2 and l2.next) or (tp.val > 9):
            l1, l2 = l1.next if l1 else None, l2.next if l2 else None
            # 计算下个节点的和，先不考虑这个节点是否进位
            tmpsum = (l1.val if l1 else 0) + (l2.val if l2 else 0)
            # 计算新链表下个节点的值（当前节点的进位+当前l1 l2的值之和），先不做进位，//表示整除，抛弃余数，用于进位
            tp.next = ListNode(tp.val // 10 + tmpsum)
            # 新链表当前节点的值取个位
            tp.val %= 10
            # 新链表往后遍历一个节点
            tp = tp.next

        return newPoint


"""
输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]
"""


def create_linklist_tail(li):
    head = ListNode(li[0])
    tail = head
    for element in li[1:]:
        node = ListNode(element)
        tail.next = node
        tail = node
    return head


l1 = create_linklist_tail([1, 2, 3, 4, 5, 6, 7])
l2 = create_linklist_tail([1, 2])

res = Solution.addTwoNumbers(l1, l2)
print(res)

while res.next:
    print(res.val)
    res = res.next
