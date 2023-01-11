import unittest
from unittest.mock import Mock
from src import AdaptiveList

class TestAdaptiveList(unittest.TestCase):
    def setUp(self) -> None:
        self.master_frame = Mock()
        self.master_frame.pack()
        self.new_frame = Mock()
        self.al = AdaptiveList(self.master_frame, self.new_frame)
        self.mock_items = [Mock(), Mock(), Mock()]

    def test_frame_property_works(self):
        self.assertEqual(self.al.frame, self.new_frame)

    def test_len_works(self):
        self.assertTrue(isinstance(len(self.al), int))

    def test_get_items_returns_a_list(self):
        self.assertEqual(type(self.al.get_items()), list)

    def test_added_item_shows_up_in_returned_list(self):
        self.al.add_item(self.mock_items[0])
        return_list = self.al.get_items()
        self.assertTrue(self.mock_items[0] in return_list)

    def test_multiple_added_items_all_show_up_in_returned_list(self):
        self.al.add_item(self.mock_items[0])
        self.al.add_item(self.mock_items[1])
        self.al.add_item(self.mock_items[2])
        return_list = self.al.get_items()
        for item in self.mock_items:
            self.assertTrue(item in return_list)

    def test_items_in_list_are_ordered_by_order_added(self):
        self.al.add_item(self.mock_items[0])
        self.al.add_item(self.mock_items[1])
        self.al.add_item(self.mock_items[2])
        return_list = self.al.get_items()
        for i, item in enumerate(self.mock_items):
            self.assertEqual(item, return_list[i])

    def test_set_item_sets_item_at_index(self):
        self.al.add_item(self.mock_items[0])
        self.al.add_item(self.mock_items[1])
        self.al.add_item(self.mock_items[2])
        new_item = Mock()
        self.al.set_item(1, new_item)
        return_list = self.al.get_items()
        self.assertEqual(new_item, return_list[1])

    def test_pack_maps_widget_frame(self):
        self.al.pack()
        self.new_frame.pack.assert_called()
    
    def test_pack_maps_list_items(self):
        self.al.add_item(self.mock_items[0])
        self.al.add_item(self.mock_items[1])
        self.al.add_item(self.mock_items[2])
        self.al.pack()
        for item in self.mock_items:
            item.grid.assert_called()

    def test_remove_item_removes_and_disables_item_in_list(self):
        self.al.add_item(self.mock_items[0])
        self.al.remove_item(0)
        return_list = self.al.get_items()
        self.assertFalse(self.mock_items[0] in return_list)

    def test_remove_item_disables_item(self):
        self.al.add_item(self.mock_items[0])
        self.al.remove_item(0)
        self.mock_items[0].grid_forget.assert_called()
    
    def test_remove_item_disables_and_removes_item_at_index(self):
        self.al.add_item(self.mock_items[0])
        self.al.add_item(self.mock_items[1])
        self.al.add_item(self.mock_items[2])
        self.al.remove_item(1)
        self.mock_items[0].grid_forget.assert_not_called()
        self.mock_items[1].grid_forget.assert_called()
        self.mock_items[2].grid_forget.assert_not_called()
        return_list = self.al.get_items()
        self.assertFalse(self.mock_items[1] in return_list)
