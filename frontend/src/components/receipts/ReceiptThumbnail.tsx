import { FileText } from 'lucide-react'
import { getReceiptFileUrl } from '../../api/receipts'
import type { ReceiptOut } from '../../types'

interface Props {
  receipt: ReceiptOut
}

export default function ReceiptThumbnail({ receipt }: Props) {
  const url = getReceiptFileUrl(receipt.id)
  const isImage = receipt.mime_type.startsWith('image/')

  if (isImage) {
    return (
      <a href={url} target="_blank" rel="noopener noreferrer" title={receipt.original_filename}>
        <img
          src={url}
          alt={receipt.original_filename}
          className="w-10 h-10 object-cover rounded border border-slate-200 hover:opacity-75 transition-opacity"
        />
      </a>
    )
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      title={receipt.original_filename}
      className="flex items-center justify-center w-10 h-10 rounded border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
    >
      <FileText className="w-5 h-5 text-slate-400" />
    </a>
  )
}
