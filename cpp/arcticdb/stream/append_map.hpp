/* Copyright 2023 Man Group Operations Limited
 *
 * Use of this software is governed by the Business Source License 1.1 included in the
 * file licenses/BSL.txt.
 *
 * As of the Change Date specified in that file, in accordance with the Business Source
 * License, use of this software will be governed by the Apache License, version 2.0.
 */

#pragma once

#include <arcticdb/entity/types.hpp>
#include <arcticdb/entity/atom_key.hpp>
#include <arcticdb/pipeline/frame_slice.hpp>
#include <arcticdb/stream/stream_source.hpp>
#include <arcticdb/storage/store.hpp>
#include <arcticdb/pipeline/input_tensor_frame.hpp>

namespace arcticdb::pipelines {
struct PythonOutputFrame;
struct InputTensorFrame;
using FilterRange = std::variant<std::monostate, IndexRange, RowRange>;
} // namespace arcticdb::pipelines

namespace arcticdb {

std::pair<std::optional<entity::AtomKey>, size_t>
read_head(const std::shared_ptr<stream::StreamSource>& store, StreamId stream_id);

std::set<StreamId> get_incomplete_refs(const std::shared_ptr<Store>& store);

std::set<StreamId> get_incomplete_symbols(const std::shared_ptr<Store>& store);

std::set<StreamId> get_active_incomplete_refs(const std::shared_ptr<Store>& store);

std::vector<pipelines::SliceAndKey> get_incomplete(const std::shared_ptr<Store>& store,
                                                   const StreamId& stream_id,
                                                   const pipelines::FilterRange& range,
                                                   uint64_t last_row,
                                                   bool via_iteration, bool load_data);

void remove_incomplete_segments(const std::shared_ptr<Store>& store,
                                const StreamId& stream_id);

/*folly::Future<entity::VariantKey> write_incomplete_frame(
    const std::shared_ptr<Store>& store,
    const StreamId& stream_id,
    pipelines::std::shared_ptr<InputTensorFrame>& frame,
    std::optional<AtomKey>&& next_key);
*/
void write_parallel(const std::shared_ptr<Store>& store, const StreamId& stream_id,
                    const std::shared_ptr<pipelines::InputTensorFrame>& frame,
                    bool validate_index);

void write_head(const std::shared_ptr<Store>& store, const AtomKey& next_key,
                size_t total_rows);

void append_incomplete_segment(const std::shared_ptr<Store>& store,
                               const StreamId& stream_id, SegmentInMemory&& seg);

void append_incomplete(const std::shared_ptr<Store>& store, const StreamId& stream_id,
                       const std::shared_ptr<pipelines::InputTensorFrame>& frame,
                       bool validate_index);

std::optional<int64_t> latest_incomplete_timestamp(const std::shared_ptr<Store>& store,
                                                   const StreamId& stream_id);
} // namespace arcticdb
