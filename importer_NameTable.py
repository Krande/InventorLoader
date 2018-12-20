# -*- coding: utf-8 -*-

import importerSegNode

from importerSegment import SegmentReader
from importerUtils   import *
from importerSegNode import _TYP_NODE_REF_, _TYP_UINT32_A_

'''
importer_NameTable.py:
'''

__author__     = 'Jens M. Plonka'
__copyright__  = 'Copyright 2018, Germany'
__url__        = "https://www.github.com/jmplonka/InventorLoader"

#TODO:
#    E9132E94 is a name table entry

class NameTableReader(SegmentReader): # for BRep and DC
	def __init__(self, segment):
		super(NameTableReader, self).__init__(segment)

	def ReadHeaderNameTableRootNode(self, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = self.ReadList2U32(node)
		i = node.ReadUInt32A(i, 2, 'from') # or is it face 1?
		i = node.ReadUInt32A(i, 2, 'to')   # or is it face 2?
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst1', 2)
		i = self.ReadU32U32U8List(node, i, 'lst2')
		i = self.skipBlockSize(i)
		node.ntEntry = True
		return i

	def ReadHeaderNameTableOtherNode(self, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = self.ReadList2U32(node)
		i = self.skipBlockSize(i)
		node.ntEntry = True
		return i

	def ReadHeaderNameTableChild1Node(self, node, typeName = None):
		i = node.Read_Header0(typeName)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, _TYP_NODE_REF_, 'lst0')
		node.ntEntry = True
		return i

	def ReadHeaderNameTableChild2Node(self, node, typeName = None):
		i = self.ReadHeaderNameTableChild1Node(node, typeName)
		i = node.ReadUInt32A(i, 7, 'a0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadList2(i, _TYP_UINT32_A_, 'lst1', 2)
		return i

	def Read_05C619B6(self, node):
		i = self.ReadHeaderNameTableOtherNode(node)
		i = node.ReadUInt8(i, 'u8_2')
		i = self.ReadU32U32List(node, i, 'a1')
		i = node.ReadUInt32A(i, 2, 'val_key_3')
		i = self.ReadU32U32U8List(node, i, 'a2')
		i = self.ReadU32U32D64List(node, i, 'a3')
		i = self.ReadU32U32D64List(node, i, 'a4')
		if (getFileVersion() > 2010): i += 16
		return i

	def Read_436D821A(self, node):
		i = self.ReadHeaderNameTableOtherNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst1', 2)
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst2', 2)
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt16A(i, 5, 'a1')
		i = node.ReadUInt8(i, 'u8_1')
		return i

	# The name table itself

	def Read_CCE92042(self, node): # NameTable
		i = node.Read_Header0('NameTable')
		i = node.ReadChildRef(i, 'cld_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'lastIdx')
		cnt, i = getUInt32(node.data, i) # strange mapping of U32 and REF
		lst = {}
		for j in range(cnt):
			key, i = getUInt32(node.data, i)
			val, i = self.ReadNodeRef(node, i, key, importerSegNode.SecNodeRef.TYPE_CHILD, 'entries')
			lst[key] = val
		node.set('entries', lst)
		return i

	# Root name table entries

	def Read_00E41C0E(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadCrossRef(i, 'ref_3')
		i = node.ReadUInt32(i, 'u32_3')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadUInt8(i, 'u8_2')
		i = node.ReadUInt32A(i, 5, 'a2')
		i = node.ReadFloat64_3D(i, 'a3')
		return i

	def Read_14340ADB(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst2', 2)
		i = node.ReadUInt32A(i, 2, 'edge') # or is it face 1?
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 7)
		return i

	def Read_22178C64(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst4', 5)
		return i

	def Read_40236C89(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 2, 'a1')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt32A(i, 3, 'a2')
		return i

	def Read_488C5309(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst2', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt32A(i, 4, 'a1')
		return i

	def Read_606D9AB1(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		return i

	def Read_6E2BCB60(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_4')
		i = node.ReadUInt32(i, 'u32_5')
		i = node.ReadFloat64(i, 'f64_0')
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_9BB4281C(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 3, 'a1')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a2')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a3')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a4')
		i = node.ReadUInt32A(i, 3, 'a5')
		return i

	def Read_BF32E0A6(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = self.ReadU32U32List(node, i, 'lst3')
		return i

	def Read_D4BDEE88(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst2', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = node.ReadUInt32A(i, 3, 'a2')
		return i

	def Read_F4360D18(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 3, 'a1')
		node.content += u" a2=[] a3=[] a4=[] a5=[0000,0000,0000]"
		node.set('a2', [])
		node.set('a3', [])
		node.set('a4', [])
		node.set('a5', [0,0,0])
		return i

	def Read_F7693D55(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_4')
		return i

	def Read_FF46726C(self, node): # Name table root node
		i = self.ReadHeaderNameTableRootNode(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst3', 2)
		i = node.ReadUInt32A(i, 2, 'edge')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_4')
		i = node.ReadUInt16(i, 'u16_1')
		return i

	# Child name table entries

	def Read_0645C2A5(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = self.ReadRefU32List(node, i, 'lst2')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadUInt32(i, 'u32_0')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a2')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a3')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a4')
		i = node.ReadUInt32A(i, 3, 'a5')
		return i

	def Read_0811C56E(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = node.ReadUInt32(i, 'u32_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt32A(i, 4, 'a1')
		if (getFileVersion() > 2011): i += 1
		return i

	def Read_2E04A208(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = self.skipBlockSize(i)
		node.content += u" lst2=[]"
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadUInt32A(i, 2, 'a2')
		cnt, i = getUInt32(node.data, i)
		i = node.ReadUInt32A(i, cnt, 'a3')
		i = node.ReadUInt32A(i, 3, 'a4')
		return i

	def Read_31D7A200(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = node.ReadUInt32(i, 'u32_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadFloat64(i, 'f64_0')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt32(i, 'u32_3')
		return i

	def Read_36895B07(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		return i

	def Read_896A9790(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_8E5D4198(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = node.ReadUInt32(i, 'u32_1')
		i = self.skipBlockSize(i)
		if (node.get('u32_1') == 0):
			i = node.ReadUInt8(i, 'u8_0')
			cnt, i = getUInt32(node.data, i)
			i = node.ReadUInt32A(i, cnt, 'a1')
			cnt, i = getUInt32(node.data, i)
			i = node.ReadUInt32A(i, cnt, 'a2')
			i = node.ReadUInt32A(i, 2, 'a3')
			i = node.ReadUInt8(i, 'u8_1')
		else:
			if(getFileVersion() > 2010):
				i = node.ReadCrossRef(i, 'ref_1')
			i = node.ReadUInt32(i, 'u32_0')
			i = self.skipBlockSize(i)
		return i

	def Read_90F4820A(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild2Node(node)
		i = self.skipBlockSize(i)
		node.content += u" lst2=[]"
		i = node.ReadUInt32A(i, 3, 'a1')
		node.content += u" a2=[0000,0000] a3=[] a4=[0000,0000,0000]"
		node.set('lst2', [])
		node.set('a2', [0,0])
		node.set('a3', [])
		node.set('a4', [0,0,0])
		return i

	def Read_B1ED010F(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild1Node(node)
		i = node.ReadUInt32A(i, 7, 'a0')
		i = node.ReadUInt32A(i, 2, 'from') # or is it face 1?
		i = self.ReadU32U32List(node, i, 'a1')
		return i

	def Read_BDE13180(self, node): # Name table child node
		i = self.ReadHeaderNameTableChild1Node(node)
		return i

	# unknown name table entries
