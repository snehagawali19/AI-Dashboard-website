export default function SkeletonCard() {
  return (
    <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden animate-pulse">
      <div className="h-40 bg-gray-100" />
      <div className="p-5 space-y-3">
        <div className="flex gap-2">
          <div className="h-5 w-16 bg-gray-100 rounded-full" />
          <div className="h-5 w-24 bg-gray-100 rounded-full" />
        </div>
        <div className="h-4 bg-gray-100 rounded w-full" />
        <div className="h-4 bg-gray-100 rounded w-3/4" />
        <div className="h-3 bg-gray-50 rounded w-full" />
        <div className="h-3 bg-gray-50 rounded w-2/3" />
        <div className="h-px bg-gray-50 mt-4" />
        <div className="flex justify-between pt-1">
          <div className="h-4 w-28 bg-gray-100 rounded" />
          <div className="flex gap-2">
            <div className="h-6 w-6 bg-gray-100 rounded-lg" />
            <div className="h-6 w-6 bg-gray-100 rounded-lg" />
          </div>
        </div>
      </div>
    </div>
  );
}
