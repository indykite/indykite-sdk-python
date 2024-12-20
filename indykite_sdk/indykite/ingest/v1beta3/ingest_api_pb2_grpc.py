# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from indykite_sdk.indykite.ingest.v1beta3 import ingest_api_pb2 as indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2


class IngestAPIStub(object):
    """IngestAPI represents the service interface for data ingestion.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamRecords = channel.stream_stream(
                '/indykite.ingest.v1beta3.IngestAPI/StreamRecords',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsResponse.FromString,
                )
        self.IngestRecord = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/IngestRecord',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordResponse.FromString,
                )
        self.BatchUpsertNodes = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchUpsertNodes',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesResponse.FromString,
                )
        self.BatchUpsertRelationships = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchUpsertRelationships',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsResponse.FromString,
                )
        self.BatchDeleteNodes = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodes',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesResponse.FromString,
                )
        self.BatchDeleteRelationships = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteRelationships',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsResponse.FromString,
                )
        self.BatchDeleteNodeProperties = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodeProperties',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesResponse.FromString,
                )
        self.BatchDeleteRelationshipProperties = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteRelationshipProperties',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesResponse.FromString,
                )
        self.BatchDeleteNodeTags = channel.unary_unary(
                '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodeTags',
                request_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsRequest.SerializeToString,
                response_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsResponse.FromString,
                )


class IngestAPIServicer(object):
    """IngestAPI represents the service interface for data ingestion.
    """

    def StreamRecords(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IngestRecord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchUpsertNodes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchUpsertRelationships(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteNodes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteRelationships(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteNodeProperties(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteRelationshipProperties(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteNodeTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IngestAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StreamRecords': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamRecords,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsResponse.SerializeToString,
            ),
            'IngestRecord': grpc.unary_unary_rpc_method_handler(
                    servicer.IngestRecord,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordResponse.SerializeToString,
            ),
            'BatchUpsertNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchUpsertNodes,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesResponse.SerializeToString,
            ),
            'BatchUpsertRelationships': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchUpsertRelationships,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsResponse.SerializeToString,
            ),
            'BatchDeleteNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteNodes,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesResponse.SerializeToString,
            ),
            'BatchDeleteRelationships': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteRelationships,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsResponse.SerializeToString,
            ),
            'BatchDeleteNodeProperties': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteNodeProperties,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesResponse.SerializeToString,
            ),
            'BatchDeleteRelationshipProperties': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteRelationshipProperties,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesResponse.SerializeToString,
            ),
            'BatchDeleteNodeTags': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteNodeTags,
                    request_deserializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsRequest.FromString,
                    response_serializer=indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'indykite.ingest.v1beta3.IngestAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IngestAPI(object):
    """IngestAPI represents the service interface for data ingestion.
    """

    @staticmethod
    def StreamRecords(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/indykite.ingest.v1beta3.IngestAPI/StreamRecords',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.StreamRecordsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IngestRecord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/IngestRecord',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.IngestRecordResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchUpsertNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchUpsertNodes',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertNodesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchUpsertRelationships(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchUpsertRelationships',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchUpsertRelationshipsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodes',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteRelationships(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteRelationships',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteNodeProperties(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodeProperties',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodePropertiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteRelationshipProperties(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteRelationshipProperties',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteRelationshipPropertiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteNodeTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/indykite.ingest.v1beta3.IngestAPI/BatchDeleteNodeTags',
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsRequest.SerializeToString,
            indykite_dot_ingest_dot_v1beta3_dot_ingest__api__pb2.BatchDeleteNodeTagsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
