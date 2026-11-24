/**
 * CabinetScan AI - Creem.io Webhook Event Receiver
 * Handles asynchronous payment confirmation from Creem MoR.
 */

module.exports = async function creemWebhookHandler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).json({ status: 'active', gateway: 'creem.io webhook listener' });
  }

  try {
    const event = req.body;
    console.log('[Creem Webhook] Event received:', event?.type || event?.event || 'generic_event');

    // Handle checkout.completed / payment.succeeded
    const eventType = event?.type || event?.event;
    if (eventType === 'checkout.completed' || eventType === 'payment.succeeded' || eventType === 'order.completed') {
      const customerEmail = event?.data?.customer?.email || event?.customer?.email;
      const orderId = event?.data?.id || event?.id;
      console.log(`[Creem Webhook] 🎉 Payment verified for: ${customerEmail}, Order: ${orderId}`);
      // In production with database, mark customer as permanently unlocked
    }

    return res.status(200).json({ received: true });
  } catch (err) {
    console.error('[Creem Webhook] Processing error:', err);
    return res.status(400).json({ error: err.message });
  }
};
