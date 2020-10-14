// service definition.

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.23.0
// 	protoc        v3.13.0
// source: option.proto

package option

import (
	context "context"
	proto "github.com/golang/protobuf/proto"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// This is a compile-time assertion that a sufficiently up-to-date version
// of the legacy proto package is being used.
const _ = proto.ProtoPackageIsVersion4

// The request message containing params
type ComputeRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Params []float32 `protobuf:"fixed32,1,rep,packed,name=params,proto3" json:"params,omitempty"`
}

func (x *ComputeRequest) Reset() {
	*x = ComputeRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_option_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ComputeRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ComputeRequest) ProtoMessage() {}

func (x *ComputeRequest) ProtoReflect() protoreflect.Message {
	mi := &file_option_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ComputeRequest.ProtoReflect.Descriptor instead.
func (*ComputeRequest) Descriptor() ([]byte, []int) {
	return file_option_proto_rawDescGZIP(), []int{0}
}

func (x *ComputeRequest) GetParams() []float32 {
	if x != nil {
		return x.Params
	}
	return nil
}

// The response message containing the greetings
type UxtSlice struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	U []*Uxt `protobuf:"bytes,1,rep,name=U,proto3" json:"U,omitempty"`
}

func (x *UxtSlice) Reset() {
	*x = UxtSlice{}
	if protoimpl.UnsafeEnabled {
		mi := &file_option_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UxtSlice) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UxtSlice) ProtoMessage() {}

func (x *UxtSlice) ProtoReflect() protoreflect.Message {
	mi := &file_option_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UxtSlice.ProtoReflect.Descriptor instead.
func (*UxtSlice) Descriptor() ([]byte, []int) {
	return file_option_proto_rawDescGZIP(), []int{1}
}

func (x *UxtSlice) GetU() []*Uxt {
	if x != nil {
		return x.U
	}
	return nil
}

type Uxt struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Ut []float32 `protobuf:"fixed32,1,rep,packed,name=Ut,proto3" json:"Ut,omitempty"`
}

func (x *Uxt) Reset() {
	*x = Uxt{}
	if protoimpl.UnsafeEnabled {
		mi := &file_option_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Uxt) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Uxt) ProtoMessage() {}

func (x *Uxt) ProtoReflect() protoreflect.Message {
	mi := &file_option_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Uxt.ProtoReflect.Descriptor instead.
func (*Uxt) Descriptor() ([]byte, []int) {
	return file_option_proto_rawDescGZIP(), []int{2}
}

func (x *Uxt) GetUt() []float32 {
	if x != nil {
		return x.Ut
	}
	return nil
}

var File_option_proto protoreflect.FileDescriptor

var file_option_proto_rawDesc = []byte{
	0x0a, 0x0c, 0x6f, 0x70, 0x74, 0x69, 0x6f, 0x6e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x28,
	0x0a, 0x0e, 0x43, 0x6f, 0x6d, 0x70, 0x75, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x12, 0x16, 0x0a, 0x06, 0x70, 0x61, 0x72, 0x61, 0x6d, 0x73, 0x18, 0x01, 0x20, 0x03, 0x28, 0x02,
	0x52, 0x06, 0x70, 0x61, 0x72, 0x61, 0x6d, 0x73, 0x22, 0x1e, 0x0a, 0x08, 0x55, 0x78, 0x74, 0x53,
	0x6c, 0x69, 0x63, 0x65, 0x12, 0x12, 0x0a, 0x01, 0x55, 0x18, 0x01, 0x20, 0x03, 0x28, 0x0b, 0x32,
	0x04, 0x2e, 0x55, 0x78, 0x74, 0x52, 0x01, 0x55, 0x22, 0x15, 0x0a, 0x03, 0x55, 0x78, 0x74, 0x12,
	0x0e, 0x0a, 0x02, 0x55, 0x74, 0x18, 0x01, 0x20, 0x03, 0x28, 0x02, 0x52, 0x02, 0x55, 0x74, 0x32,
	0x3d, 0x0a, 0x0d, 0x4f, 0x70, 0x74, 0x69, 0x6f, 0x6e, 0x50, 0x72, 0x69, 0x63, 0x69, 0x6e, 0x67,
	0x12, 0x2c, 0x0a, 0x0c, 0x43, 0x6f, 0x6d, 0x70, 0x75, 0x74, 0x65, 0x50, 0x72, 0x69, 0x63, 0x65,
	0x12, 0x0f, 0x2e, 0x43, 0x6f, 0x6d, 0x70, 0x75, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x1a, 0x09, 0x2e, 0x55, 0x78, 0x74, 0x53, 0x6c, 0x69, 0x63, 0x65, 0x22, 0x00, 0x42, 0x0a,
	0x5a, 0x08, 0x2e, 0x3b, 0x6f, 0x70, 0x74, 0x69, 0x6f, 0x6e, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x33,
}

var (
	file_option_proto_rawDescOnce sync.Once
	file_option_proto_rawDescData = file_option_proto_rawDesc
)

func file_option_proto_rawDescGZIP() []byte {
	file_option_proto_rawDescOnce.Do(func() {
		file_option_proto_rawDescData = protoimpl.X.CompressGZIP(file_option_proto_rawDescData)
	})
	return file_option_proto_rawDescData
}

var file_option_proto_msgTypes = make([]protoimpl.MessageInfo, 3)
var file_option_proto_goTypes = []interface{}{
	(*ComputeRequest)(nil), // 0: ComputeRequest
	(*UxtSlice)(nil),       // 1: UxtSlice
	(*Uxt)(nil),            // 2: Uxt
}
var file_option_proto_depIdxs = []int32{
	2, // 0: UxtSlice.U:type_name -> Uxt
	0, // 1: OptionPricing.ComputePrice:input_type -> ComputeRequest
	1, // 2: OptionPricing.ComputePrice:output_type -> UxtSlice
	2, // [2:3] is the sub-list for method output_type
	1, // [1:2] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_option_proto_init() }
func file_option_proto_init() {
	if File_option_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_option_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ComputeRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_option_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UxtSlice); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_option_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Uxt); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_option_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   3,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_option_proto_goTypes,
		DependencyIndexes: file_option_proto_depIdxs,
		MessageInfos:      file_option_proto_msgTypes,
	}.Build()
	File_option_proto = out.File
	file_option_proto_rawDesc = nil
	file_option_proto_goTypes = nil
	file_option_proto_depIdxs = nil
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConnInterface

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// OptionPricingClient is the client API for OptionPricing service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type OptionPricingClient interface {
	// Method to compute option price
	ComputePrice(ctx context.Context, in *ComputeRequest, opts ...grpc.CallOption) (*UxtSlice, error)
}

type optionPricingClient struct {
	cc grpc.ClientConnInterface
}

func NewOptionPricingClient(cc grpc.ClientConnInterface) OptionPricingClient {
	return &optionPricingClient{cc}
}

func (c *optionPricingClient) ComputePrice(ctx context.Context, in *ComputeRequest, opts ...grpc.CallOption) (*UxtSlice, error) {
	out := new(UxtSlice)
	err := c.cc.Invoke(ctx, "/OptionPricing/ComputePrice", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// OptionPricingServer is the server API for OptionPricing service.
type OptionPricingServer interface {
	// Method to compute option price
	ComputePrice(context.Context, *ComputeRequest) (*UxtSlice, error)
}

// UnimplementedOptionPricingServer can be embedded to have forward compatible implementations.
type UnimplementedOptionPricingServer struct {
}

func (*UnimplementedOptionPricingServer) ComputePrice(context.Context, *ComputeRequest) (*UxtSlice, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ComputePrice not implemented")
}

func RegisterOptionPricingServer(s *grpc.Server, srv OptionPricingServer) {
	s.RegisterService(&_OptionPricing_serviceDesc, srv)
}

func _OptionPricing_ComputePrice_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ComputeRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(OptionPricingServer).ComputePrice(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/OptionPricing/ComputePrice",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(OptionPricingServer).ComputePrice(ctx, req.(*ComputeRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _OptionPricing_serviceDesc = grpc.ServiceDesc{
	ServiceName: "OptionPricing",
	HandlerType: (*OptionPricingServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "ComputePrice",
			Handler:    _OptionPricing_ComputePrice_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "option.proto",
}
